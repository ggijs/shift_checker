import checker

shift_checker = checker.Shift_checker()

def main():
    shift_checker.run()

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('Shutting down')