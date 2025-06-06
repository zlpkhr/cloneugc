require "open3"

class NormalizeActorClipJob < ApplicationJob
  queue_as :default

  def perform(actor_id)
    actor = Actor.find_by(id: actor_id)
    return unless actor&.clip&.attached?

    original_clip = actor.clip

    Dir.mktmpdir do |tmpdir|
      original_path = File.join(tmpdir, original_clip.filename.to_s)

      File.open(original_path, "wb") do |file|
        original_clip.download { |chunk| file.write(chunk) }
      end

      video = Video.new(original_path)
      return if video.container == "ISOBMFF"

      normalized_filename = "#{SecureRandom.uuid}.mp4"
      processed_path = File.join(tmpdir, normalized_filename)

      command = build_normalize_command(original_path, processed_path)

      stdout, stderr, status = Open3.capture3(command)
      Rails.logger.debug { "ffmpeg output for Actor##{actor.id}:\nSTDOUT:\n#{stdout}\nSTDERR:\n#{stderr}" }

      if status.success? && File.exist?(processed_path)
        actor.clip.attach(
          io: File.open(processed_path),
          filename: normalized_filename,
          content_type: "video/mp4"
        )
      else
        Rails.logger.error { "ffmpeg command failed for Actor##{actor.id}:\nSTDOUT:\n#{stdout}\nSTDERR:\n#{stderr}" }
      end
    end
  end

  private

  def build_normalize_command(input_path, output_path)
    "ffmpeg -y -i #{Shellwords.escape(input_path)} -preset fast -crf 23 -c:v libx264 -c:a aac -movflags +faststart #{Shellwords.escape(output_path)}"
  end
end
