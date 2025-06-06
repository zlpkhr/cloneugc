require "test_helper"

class NormalizeActorClipJobTest < ActiveJob::TestCase
  test "should normalize non-mp4 clips" do
    actor = Actor.new
    actor.clip.attach(io: File.open(Rails.root.join("test/fixtures/files/azamat.mov")), filename: "azamat.mov")
    actor.save(validate: false)

    original_blob_id = actor.clip.blob.id

    perform_enqueued_jobs do
      NormalizeActorClipJob.perform_later(actor.id)
    end

    actor.reload

    assert_not_equal original_blob_id, actor.clip.blob.id

    actor.clip.blob.open do |tempfile|
      video = Video.new(tempfile.path)
      assert_equal "ISOBMFF", video.container
    end
  end

  test "should skip mp4 clips" do
    actor = Actor.new
    actor.clip.attach(io: File.open(Rails.root.join("test/fixtures/files/azamat.mp4")), filename: "azamat.mp4")
    actor.save(validate: false)

    original_blob_id = actor.clip.blob.id

    perform_enqueued_jobs do
      NormalizeActorClipJob.perform_later(actor.id)
    end

    actor.reload
    assert_equal original_blob_id, actor.clip.blob.id
  end
end
