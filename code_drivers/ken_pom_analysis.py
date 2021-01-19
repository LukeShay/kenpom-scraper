from data.ken_pom import ken_pom_data


def main():
    print("Dog under 70: {}".format(ken_pom_data.dog_under_percent(70)[2]))
    print("Dog under 75: {}".format(ken_pom_data.dog_under_percent(75)[2]))
    print("Dog under 80: {}".format(ken_pom_data.dog_under_percent(80)[2]))
    print("Dog under 85: {}".format(ken_pom_data.dog_under_percent(85)[2]))
    print("Dog under 90: {}".format(ken_pom_data.dog_under_percent(90)[2]))


if __name__ == "__main__":
    main()
