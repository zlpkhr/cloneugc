class ExtractActorAttributesJob < ApplicationJob
  queue_as :default

  def perform(actor_id)
    actor = Actor.find(actor_id)
    unless actor.clip.attached?
      Rails.logger.info("Actor #{actor.id} has no clip attached.")
      return
    end

    blob = nil
    begin
      Dir.mktmpdir do |dir|
        frame_name = "#{SecureRandom.uuid}.jpg"
        frame_path = File.join(dir, frame_name)

        actor.clip.blob.open do |video_file|
          command = build_extract_frame_command(video_file.path, frame_path)
          stdout, stderr, status = Open3.capture3(command)

          unless status.success?
            Rails.logger.error("ffmpeg command failed for Actor##{actor.id}:\nSTDOUT:\n#{stdout}\nSTDERR:\n#{stderr}")
          end
        end

        unless File.exist?(frame_path)
          Rails.logger.warn("ExtractActorAttributesJob: Could not extract frame for actor #{actor.id}")
          return
        end

        blob = ActiveStorage::Blob.create_and_upload!(
          io: File.open(frame_path),
          filename: frame_name,
          content_type: "image/jpeg"
        )

        image_url = blob.url(expires_in: 5.minutes)

        provider = Llm::Providers::Openai.new(Secrets.get_plaintext("openai-api-key"))
        llm = Llm.new(provider)

        attributes = llm.extract_person_attributes(image_url)

        actor.update!(attributes)
      end
    rescue StandardError => e
      Rails.logger.error("ExtractActorAttributesJob failed for actor #{actor.id}: #{e.message}")
      # Re-raising the exception to allow for retry mechanisms from the job runner.
      raise e
    ensure
      blob&.purge
    end
  end

  private

    def build_extract_frame_command(input_path, output_path)
      "ffmpeg -v error -ss 0 -i #{Shellwords.escape(input_path)} -frames:v 1 -q:v 2 -y #{Shellwords.escape(output_path)}"
    end
end
