from datalad.tests.utils import assert_result_count


def test_register():
    import datalad.api as da
    assert hasattr(da, 'lgpd_extension')
    assert_result_count(
        da.lgpd_extension(),
        1,
        action='demo')

