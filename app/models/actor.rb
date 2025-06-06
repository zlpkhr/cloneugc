class Actor < ApplicationRecord
  has_one_attached :clip

  enum gender: { male: "Male", female: "Female" }
  enum ethnicity: {
    asian: "Asian",
    black: "Black",
    white: "White",
    hispanic: "Hispanic",
    middle_eastern: "Middle Eastern"
  }
  enum age_group: {
    young_adult: "Young Adult",
    middle_aged: "Middle Aged",
    senior: "Senior"
  }

  validates :clip,
    attached: true,
    content_type: { with: /\Avideo\/.*\z/ },
    aspect_ratio: { with: :portrait },
    duration: { between: 15.seconds..3.minutes }
end
