from MrBam.count import count_different_type
from argparse import Namespace

def test_count_different_type_1():
    "it should NOT count dna that more than 10% reads have different bases"

    o = Namespace(verbos=False, allow_inconsist=False)

    pair = {
        ('ref', 2, True): [
            ('A', 60),
            ('T', 60),
            ('T', 60)
        ],
        ('ref', 3, False): [
            ('A', 60),
            ('T', 60),
            ('T', 60)
        ]
    }

    mor, mnr, msr, oor, onr, osr, moa, mna, msa, ooa, ona, osa, inconsis = count_different_type(o, pair, {}, 'T', 'A')

    assert inconsis == 6
    assert sum((mor, mnr, msr, oor, onr, osr, moa, mna, msa, ooa, ona, osa)) == 0

def test_count_different_type_2():
    "basic non-trival test case"

    o = Namespace(verbos=False, allow_inconsist=False)

    pair = {
        ('ref', 2, True): [
            ('A', 60),
            ('A', 60)
        ],
        ('ref', 3, False): [
            ('T', 60),
            ('T', 60),
            ('T', 60)
        ],
        ('ref', 4, False): [
            ('T', 60),
        ]
    }

    single = {
        ('ref', 2, True): [
            ('T', 60),
            ('A', 60)
        ],
        ('ref', 3, False): [
            ('T', 60),
            ('T', 60),
            ('T', 60)
        ],
        ('ref', 4, False): [
            ('A', 60),
        ]
    }

    mor, mnr, msr, oor, onr, osr, moa, mna, msa, ooa, ona, osa, inconsis = count_different_type(o, pair, single, 'T', 'A')

    assert mor == 1
    assert mnr == 0
    assert msr == 0
    assert oor == 0
    assert onr == 0
    assert osr == 1
    assert moa == 0
    assert mna == 1
    assert msa == 1
    assert ooa == 0
    assert ona == 1
    assert osa == 0
    assert inconsis == 2

def test_count_different_type_3():
    "allow inconsis"

    o = Namespace(verbos=False, allow_inconsist=True)

    pair = {
        ('ref', 2, True): [
            ('A', 60),
            ('T', 60),
            ('T', 60)
        ],
        ('ref', 3, False): [
            ('A', 60),
            ('T', 60),
            ('T', 60)
        ]
    }

    mor, mnr, msr, oor, onr, osr, moa, mna, msa, ooa, ona, osa, inconsis = count_different_type(o, pair, {}, 'T', 'A')

    assert mor == 0
    assert mnr == 0
    assert msr == 0
    assert oor == 1
    assert onr == 1
    assert osr == 0
    assert moa == 1
    assert mna == 1
    assert msa == 0
    assert ooa == 0
    assert ona == 0
    assert osa == 0
    assert inconsis == 0
