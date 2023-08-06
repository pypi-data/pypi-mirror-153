class DeveloperError(Exception):
    """
    An exception which indicates a developer error. This is used instead of assertions in testcases because if
    one were to check for AssertionErrors and an assertion is raised not because of a tested condition, but
    because the test-utils were used incorrectly, then there is no way to distinguish between those.

    Use only in testcases, use normal assertions for service code. you can still use assertions in
    setUp(), tearDown(), setUpClass(), tearDownClass() code, because nobody would catch assertions there
    """
