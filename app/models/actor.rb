class Actor < ApplicationRecord
  has_one_attached :clip

  GENDER = [ "male", "female" ]
  ETHNICITIES = [ "asian", "black", "white", "hispanic", "middle_eastern" ]
  AGE_GROUPS = [ "young_adult", "middle_aged", "senior" ]

  validates :clip,
    attached: true,
    content_type: { with: /\Avideo\/.*\z/ },
    aspect_ratio: { with: :portrait },
    duration: { between: 15.seconds..3.minutes }
  validates :gender, inclusion: { in: GENDER }
  validates :ethnicity, inclusion: { in: ETHNICITIES }
  validates :age_group, inclusion: { in: AGE_GROUPS }
end
