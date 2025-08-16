ppm = PreProductionManager(studio)

while not ppm.is_done():
    step = ppm.get_prompt()
    gui.show_prompt(step["prompt"], step["choices"])
    
    # In GUI, you’d wait for the user to click a choice
    user_selection_index = gui.get_choice_index()
    ppm.select_choice(user_selection_index)