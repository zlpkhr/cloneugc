require "test_helper"

class ActorTest < ActiveSupport::TestCase
  test "valid male actor" do
    actor = actors(:valid_male)
    assert actor.valid?
  end

  test "valid female actor" do
    actor = actors(:valid_female)
    assert actor.valid?
  end

  test "invalid gender" do
    actor = actors(:invalid_gender)
    assert_not actor.valid?
  end

  test "invalid ethnicity" do
    actor = actors(:invalid_ethnicity)
    assert_not actor.valid?
  end

  test "invalid age group" do
    actor = actors(:invalid_age_group)
    assert_not actor.valid?
  end
end
