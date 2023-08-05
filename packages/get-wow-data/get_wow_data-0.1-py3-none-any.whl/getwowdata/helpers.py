#format the value in terms of gold, silver, and copper
def as_gold(amount):
    if amount >= 0:
        return (f"{int(str(amount)[:-4]):,}g {str(amount)[-4:-2]}s {str(amount)[-2:]}c")
    else:
        return (f"{int(str(amount)[:-4]):,}g {str(amount)[-4:-2]}s {str(amount)[-2:]}c")


