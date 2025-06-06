class Admin::ActorsController < ApplicationController
  def index
    @actors = Actor.all
  end

  def new
    @actor = Actor.new
  end

  def create
    @actor = Actor.new(actor_params)
    if @actor.save
      redirect_to admin_actors_path, notice: "Actor created successfully"
    else
      render :new
    end
  end

  private

  def actor_params
    params.require(:actor).permit(:clip)
  end
end
