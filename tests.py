import random
from Complementary import *

def test_Complement(cls):
    N = 10000
    passed = 0
    failed = 0 
    invalid = 0

    low, high = cls(0).RANGE    
    while (passed + failed) < N:
        nat1 = random.randint(low, high)
        nat2 = random.randint(low, high)
        nat_sum = nat1 + nat2

        try:
            comp1 = cls(nat1)
            comp2 = cls(nat2)
        except Exception as err:
            raise Exception("Couldn't initialize values:", err)
        
        try:
            _ = cls(nat_sum)
        except ValueError:
            invalid += 1
            continue  # our type can't handle overflows

        try:
            comp_sum = comp1 + comp2
        except Exception as err:
            print(f"Failed to sum: {comp1!r} + {comp2!r}: {err}")
            print(f"\t {comp1} + {comp2}")
            continue
        
        try:
            assert comp_sum == nat_sum, f"Test failed: {nat1}+{nat2} != {comp_sum}. Expected {nat_sum}"
            passed += 1
        except AssertionError as err:
            # print(err)
            failed += 1

    if not failed:
        print(f"All {passed} tests in range [{low}, {high}] passed!")
    else:
        print(f"Failed {failed}, passed {passed} tests")
        return False

    if invalid:
        print(f"Skipped {invalid} invalid tests")

if __name__ == "__main__":
    print(f"Testing ten complement. Range: {TenComplement(0).RANGE}")
    test_Complement(TenComplement)
    print()

    print(f"Testing hex complement. Range: {HexComplement(0).RANGE}")
    test_Complement(HexComplement)
    print()

    print(f"Testing binary complement: Range: {BinComplement(0).RANGE}")
    test_Complement(BinComplement)
    print()

    print(f"Testing seximal complement: Range: {SexComplement(0).RANGE}")
    test_Complement(SexComplement)
    print()



