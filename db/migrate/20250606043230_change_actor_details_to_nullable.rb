class ChangeActorDetailsToNullable < ActiveRecord::Migration[7.1]
  def change
    change_column_null :actors, :gender, true
    change_column_null :actors, :ethnicity, true
    change_column_null :actors, :age_group, true
  end
end
