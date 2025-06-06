class Actor < ApplicationRecord
  has_one_attached :clip

  validates :clip,
    attached: true,
    content_type: { with: /\Avideo\/.*\z/ },
    aspect_ratio: { with: :portrait },
    duration: { between: 15.seconds..3.minutes }
end
