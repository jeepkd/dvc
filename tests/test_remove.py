import os

from dvc.main import main
from dvc.stage import Stage, StageFileDoesNotExistError
from dvc.command.remove import CmdRemove

from tests.basic_env import TestDvc


class TestRemove(TestDvc):
    def test(self):
        stages = self.dvc.add(self.FOO)
        self.assertEqual(len(stages), 1)
        stage = stages[0]
        self.assertTrue(stage is not None)
        stage_removed = self.dvc.remove(stage.path, outs_only=True)

        self.assertIsInstance(stage_removed, Stage)
        self.assertEqual(stage.path, stage_removed.path)
        self.assertFalse(os.path.isfile(self.FOO))

        stage_removed = self.dvc.remove(stage.path)
        self.assertIsInstance(stage_removed, Stage)
        self.assertEqual(stage.path, stage_removed.path)
        self.assertFalse(os.path.isfile(self.FOO))
        self.assertFalse(os.path.exists(stage.path))


class TestRemoveNonExistentFile(TestDvc):
    def test(self):
        with self.assertRaises(StageFileDoesNotExistError) as cx:
            self.dvc.remove('non_existent_dvc_file')


class TestRemoveDirectory(TestDvc):
    def test(self):
        stages = self.dvc.add(self.DATA_DIR)
        self.assertEqual(len(stages), 1)
        stage_add = stages[0]
        self.assertTrue(stage_add is not None)
        stage_removed = self.dvc.remove(stage_add.path)
        self.assertEqual(stage_add.path, stage_removed.path)
        self.assertFalse(os.path.exists(self.DATA_DIR))
        self.assertFalse(os.path.exists(stage_removed.path))


class TestCmdRemove(TestDvc):
    def test(self):
        stages = self.dvc.add(self.FOO)
        self.assertEqual(len(stages), 1)
        stage = stages[0]
        self.assertTrue(stage is not None)
        ret = main(['remove',
                    stage.path])
        self.assertEqual(ret, 0)

        ret = main(['remove',
                    'non-existing-dvc-file'])
        self.assertNotEqual(ret, 0)
