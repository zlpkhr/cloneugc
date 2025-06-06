require "test_helper"

class VideoTest < ActiveSupport::TestCase
  test "should return correct container for mp4" do
    video = Video.new(Rails.root.join("test/fixtures/files/azamat.mp4"))
    assert_equal "ISOBMFF", video.container
  end

  test "should return correct container for mov" do
    video = Video.new(Rails.root.join("test/fixtures/files/azamat.mov"))
    assert_equal "QTFF", video.container
  end
end
