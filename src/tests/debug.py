if __name__ == "__main__":
    # print(["leggings", "underwear"].split(","))
    data = ["Brown", "colors_digital-seamless-leggings", "Taupe_color"]
    print(
        next(
            (item.split("_")[0].lower() for item in data if "_color" in item),
            None,
        )
    )
