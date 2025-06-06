require "test_helper"

class Admin::ActorsControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get admin_actors_url
    assert_response :success
  end

  test "should get new" do
    get new_admin_actor_url
    assert_response :success
  end

  test "should create actor with clip" do
    assert_difference("Actor.count", 1) do
      post admin_actors_url, params: {
        actor: {
          clip: fixture_file_upload(Rails.root.join("test/fixtures/files/azamat.mp4"), "video/mp4")
        }
      }
    end
  end
end
