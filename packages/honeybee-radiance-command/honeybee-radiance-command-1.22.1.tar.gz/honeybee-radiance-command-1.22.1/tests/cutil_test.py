import honeybee_radiance_command.cutil as cutil


def test_import_from_string():
    """Test import options form a string."""
    options = cutil.parse_radiance_options('-dj   20  -fo -dc 1 -ab 16    -lw 1e-8')

    assert options['dj'] == '20'
    assert options['fo'] == ''
    assert options['dc'] == '1'
    assert options['ab'] == '16'
    assert options['lw'] == '1e-8'


def test_import_view_from_string():
    """Test import options form a string."""
    view = 'rvu -vtv -vp 0.000 0.000 0.000 -vd 0.000 0.000 1.000 ' \
        '-vu 0.000 1.000 0.000 -vh 29.341 -vv 32.204 -x 300 -y 300 ' \
        '-vs -0.500 -vl -0.500 -vo 100.000'

    options = cutil.parse_radiance_options(view)
    
    assert 'rvu' not in options
    assert options['vtv'] == ''
    assert options['vp'] == ['0.000', '0.000', '0.000']
    assert options['vd'] == ['0.000', '0.000', '1.000']
    assert options['vu'] == ['0.000', '1.000', '0.000']
    assert options['vh'] == '29.341'
    assert options['vv'] == '32.204'
    assert options['x'] == '300'
    assert options['y'] == '300'
    assert options['vs'] == '-0.500'
    assert options['vl'] == '-0.500'
    assert options['vo'] == '100.000'