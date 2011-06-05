
import os
from StringIO import StringIO
from hamcrest import *
from nose.tools import raises
import deft.cli as cli
from deft.tracker import UserError, Feature
from deft.fake_tracker import fake_feature


class FindEditorCommand_Test:
    def test_prefers_deft_editor_if_set(self):
        assert_that(cli.find_editor_command({'DEFT_EDITOR': 'D', 'EDITOR': 'E', 'VISUAL': 'V'}),
                    equal_to('D'))
    
    def test_prefers_visual_if_deft_editor_not_set(self):
        assert_that(cli.find_editor_command({'EDITOR': 'E', 'VISUAL': 'V'}),
                    equal_to('V'))

    def test_will_use_editor_as_last_resort(self):
        assert_that(cli.find_editor_command({'EDITOR': 'E'}),
                    equal_to('E'))
        
    @raises(UserError)
    def test_throws_user_error_if_no_editor_specified(self):
        cli.find_editor_command({})


class FormatFeatureTable_Test:
    def test_formats_features_as_aligned_columns(self):
        features = [
            fake_feature(name="alice", status="pending", priority=1),
            fake_feature(name="bob", status="pending", priority=2),
            fake_feature(name="carol", status="active", priority=8),
            fake_feature(name="dave", status="active", priority=9),
            fake_feature(name="eve", status="active", priority=10)]
        
        output = StringIO()
        
        cli.format_feature_table(features, output)
        
        formatted_lines = output.getvalue().splitlines()
        
        assert_that(formatted_lines, equal_to([
                    "pending  1 alice",
                    "pending  2 bob",
                    "active   8 carol",
                    "active   9 dave",
                    "active  10 eve"]))
        
    def test_formats_empty_list_as_empty_string(self):
        output = StringIO()
        
        cli.format_feature_table([], output)
        
        assert_that(output.getvalue(), equal_to(""))
        
