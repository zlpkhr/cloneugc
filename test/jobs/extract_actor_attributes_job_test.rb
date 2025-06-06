require "test_helper"

class ExtractActorAttributesJobTest < ActiveJob::TestCase
  setup do
    @actor = actors(:azamat)
  end

  test "extracts attributes and updates actor" do
    perform_enqueued_jobs do
      ExtractActorAttributesJob.perform_later(@actor.id)
    end

    @actor.reload

    assert_not_nil @actor.gender
    assert_not_nil @actor.ethnicity
    assert_not_nil @actor.age_group
  end

  test "job does nothing if actor has no clip" do
    actor_without_clip = actors(:azamat_no_clip)
    assert_not actor_without_clip.clip.attached?

    perform_enqueued_jobs do
      ExtractActorAttributesJob.perform_later(actor_without_clip.id)
    end

    actor_without_clip.reload
    assert_nil actor_without_clip.gender
    assert_nil actor_without_clip.ethnicity
    assert_nil actor_without_clip.age_group
  end
end
