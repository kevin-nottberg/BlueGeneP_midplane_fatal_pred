def main():
    main_log = open("Intrepid_RAS_0901_0908_scrubbed", "r+")

    for i in range(0,10):
        print("{}: {}".format(i, main_log.readline())

if __name__ == "__main__":
    main()
