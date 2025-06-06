require "open3"
require "json"

class Video
  attr_reader :path

  def initialize(path)
    @path = path
  end

  def container
    case major_brand
    when "isom", "mp41", "mp42", "avc1", "dash"
      "ISOBMFF"
    when "qt"
      "QTFF"
    end
  end

  private

    def metadata
      @metadata ||= begin
        command = "ffprobe -v quiet -print_format json -show_format #{Shellwords.escape(path)}"
        stdout, _stderr, status = Open3.capture3(command)
        status.success? ? JSON.parse(stdout) : {}
      end
    end

    def major_brand
      metadata.dig("format", "tags", "major_brand").to_s.strip
    end
end
