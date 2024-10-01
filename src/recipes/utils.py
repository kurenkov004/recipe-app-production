from .models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt  # type: ignore
from collections import Counter


def get_graph():
    # create a BytesIO buffer for the image
    buffer = BytesIO()
    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format="png")
    # set cursor to the beginning of the stream
    buffer.seek(0)
    # retrieve the content of the file
    image_png = buffer.getvalue()
    # encode the bytes-like object
    graph = base64.b64encode(image_png)
    # decode to get the string as output
    graph = graph.decode("utf-8")
    # free up the memory of buffer
    buffer.close()

    # return the image/graph
    return graph


def get_top_ingredients_chart(recipes):
    all_ingredients = []

    for recipe in recipes:
        # split ingredients string
        ingredients_list = recipe["ingredients"].split(",")
        # clean ingredients and strip extra characters
        cleaned = [ingredient.strip().lower() for ingredient in ingredients_list]
        # add cleaned ingredients to list initialized above
        all_ingredients.extend(cleaned)

    ingredient_count = Counter(all_ingredients)
    ingredients, counts = (
        zip(*ingredient_count.most_common(5)) if all_ingredients else ([], [])
    )

    # switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    plt.switch_backend("AGG")
    # specify figure size
    plt.figure(figsize=(6, 4), facecolor="whitesmoke", edgecolor="darkslategrey")

    # create bar chart
    if ingredients and counts:
        plt.bar(ingredients, counts, color="navy")
        plt.xlabel("Ingredients")  # Label the x-axis.
        plt.ylabel("Number of Occurences")  # Label the y-axis.
        plt.title("5 Top Ingredients")  # Set the chart title.
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability.
    else:
        plt.text(
            0.5,
            0.5,
            "No data available",
            horizontalalignment="center",
            verticalalignment="center",
        )

    plt.tight_layout()
    chart = get_graph()
    plt.close()

    return chart


def get_difficulty_spread_chart(recipes):
    # count recipes by difficulty
    difficulty_spread = Counter(
        recipe["difficulty"] for recipe in recipes if "difficulty" in recipe
    )
    # switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    plt.switch_backend("AGG")
    # specify figure size
    fig = plt.figure(figsize=(6, 4), facecolor="whitesmoke")

    # plot pie chart
    if difficulty_spread:
        plt.pie(difficulty_spread.values(), labels=difficulty_spread.keys())
        plt.title("Recipe spread by difficulty level")
        plt.axis("equal")
    else:
        plt.text(
            0.5,
            0.5,
            "No data available",
            horizontalalignment="center",
            verticalalignment="center",
        )

    plt.tight_layout()
    chart = get_graph()
    plt.close()
    return chart


def get_cooking_time_by_difficulty_chart(recipes):
    # Generates a line chart showing average cooking time by difficulty level.
    # Organize recipes by difficulty and collect their cooking times.
    difficulty_levels = ["Easy", "Medium", "Intermediate", "Hard"]
    cooking_times = {difficulty: [] for difficulty in difficulty_levels}

    for recipe in recipes:
        if recipe["difficulty"] in cooking_times:
            cooking_times[recipe["difficulty"]].append(recipe["cooking_time"])

    # Calculate average cooking time for each difficulty level.
    avg_cooking_times = {
        difficulty: sum(times) / len(times) if times else 0
        for difficulty, times in cooking_times.items()
    }

    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 4), facecolor="whitesmoke")
    # Plot the line chart.
    plt.plot(
        list(avg_cooking_times.keys()),
        list(avg_cooking_times.values()),
        marker="o",
        linestyle="-",
        color="blue",
    )
    plt.title("Average Cooking Time by Difficulty")  # Set title.
    plt.xlabel("Difficulty Level")  # Label x-axis.
    plt.ylabel("Average Cooking Time (minutes)")  # Label y-axis.
    plt.grid(True)  # Add a grid for readability.
    plt.tight_layout()  # Adjust layout.

    plt.tight_layout()
    chart = get_graph()
    plt.close()
    return chart
