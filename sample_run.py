from game.studio import Studio
from game.writers import generate_writer
from game.scripts import generate_script
from game.calendar import GameCalendar

calendar = GameCalendar()
studio = Studio()

print("🎬 Welcome to HollywoodSim – Sample Run")
print("---------------------------------------")

for _ in range(6):  # Simulate 6 months
    print(f"\n📆 {calendar.get_date()}")

    writer = generate_writer()
    script = generate_script(writer)

    print(f"📝 New script available: {script['title']} (Genre: {script['genre']}, Quality: {script['quality']})")
    studio.produce_movie(script)

    studio.release_movies(calendar)
    calendar.advance_month()

print("\n🏁 End of Sample Run")
studio.print_report()
