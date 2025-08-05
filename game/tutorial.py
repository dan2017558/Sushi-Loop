import pygame
import config

helper = pygame.image.load(config.resource_path("assets/sprites/helper.png"))

steps = {
    0: ["Press 'S' to skip this tutorial", "Use < and > to navigate steps"],
    1: ["Press 'H' to toggle button hints"],
    2: ["Your goal is to reach the highest", "score possible before time runs out."],
    3: ["If the timer hits 0, the game ends", "and you'll return to the menu."],
    4: ["Gain score by satisfying the trays", "moving along the conveyor belt."],
    5: ["Each tray gives either score or time", "as a reward for completing the order."],
    6: ["Trays with a cash symbol", "increase your score."],
    7: ["Trays with a clock symbol", "add more time to the timer."],
    8: ["The exact reward amount is shown", "on the paper attached to each tray."],
    9: ["To complete a tray, drag the correct", "sushi onto it before it disappears."],
    10: ["Each tray lists its required sushi", "in yellow text on the body of the tray."],
    11: ["Making sushi is simple: drag ingredients", "onto the mat, then roll and cut."],
    12: ["To the left are 5 ingredient trays —", "each gives a specific ingredient."],
    13: ["Ingredients: Tuna, Salmon, Shrimp,", "Nori, and Rice (bottom tray)."],
    14: ["You also have tools: a mat, a knife,", "and a sauce bottle."],
    15: ["Tools: Mat = hold ingredients and roll,", "Knife = cut, Sauce = apply to sushi."],
    16: ["To move items, hold left-click and drag.", "You can only hold one item at a time."],
    17: ["Build sushi by dragging ingredients", "onto the mat in the correct order."],
    18: ["If the sushi needs sauce, drag the", "sauce bottle onto the mat and press Space."],
    19: ["After adding ingredients, grab the mat", "and press Space to roll the sushi."],
    20: ["This turns the ingredients into a roll", "that's ready to be cut."],
    21: ["To cut, drag the knife onto the roll", "and press Space."],
    22: ["Then click the sushi to flip it", "— it's now ready to serve."],
    23: ["Drag finished sushi onto trays that", "request it to complete the order."],
    24: ["Trays only accept correct sushi, so", "read the order carefully."],
    25: ["Now let's cover sushi recipes —", "these are the required steps for each in order."],
    26: ["Rice Sushi:", "Nori + Rice + Roll + Cut"],
    27: ["Tuna Sushi:", "Nori + Rice + Tuna x2 + Sauce + Roll + Cut"],
    28: ["Salmon Sushi:", "Nori + Rice + Salmon x2 + Sauce + Roll + Cut"],
    29: ["Shrimp Sushi:", "Nori + Rice + Shrimp x2 + Sauce + Roll + Cut"],
    30: ["That's everything!", "Now go have fun and aim for a high score!"],
}


def tutorial(step: int):
    config.internal_surface.blit(helper, (186, 57))  # blit helper

    for i, line in enumerate(steps[step]):  # blit instructions
        text = config.score_font.render(line, 1, (24, 20, 37))
        config.text_surface.blit(
            text, (60 * config.scale, config.INTERNAL_HEIGHT * config.scale - 25 * config.scale + (i * 8 * config.scale))
        )
