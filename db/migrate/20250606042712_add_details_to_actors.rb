class AddDetailsToActors < ActiveRecord::Migration[8.0]
  def change
    add_column :actors, :ethnicity, :string
    add_column :actors, :gender, :string
    add_column :actors, :age_group, :string
  end
end
