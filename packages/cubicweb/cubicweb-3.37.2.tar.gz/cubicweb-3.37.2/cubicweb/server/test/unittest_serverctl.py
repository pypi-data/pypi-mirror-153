import os.path as osp
import shutil
from unittest.mock import patch

from cubicweb import ExecutionError
from cubicweb.devtools import testlib, ApptestConfiguration
from cubicweb.server.serverconfig import ServerConfiguration
from cubicweb.server.serverctl import (
    DBDumpCommand,
    RepositorySchedulerCommand,
    SynchronizeSourceCommand,
    repo_cnx,
)


class ServerCTLTC(testlib.CubicWebTC):
    def setUp(self):
        super().setUp()
        self.orig_config_for = ServerConfiguration.config_for

        def config_for(appid):
            return ApptestConfiguration(appid, __file__)

        ServerConfiguration.config_for = staticmethod(config_for)

    def tearDown(self):
        ServerConfiguration.config_for = self.orig_config_for
        super().tearDown()

    def test_dump(self):
        DBDumpCommand(None).run([self.appid])
        shutil.rmtree(osp.join(self.config.apphome, "backup"))

    def test_scheduler(self):
        cmd = RepositorySchedulerCommand(None)
        with patch(
            "sched.scheduler.run", side_effect=RuntimeError("boom")
        ) as patched_run:
            with self.assertRaises(RuntimeError) as exc_cm:
                with self.assertLogs("cubicweb.repository", level="INFO") as log_cm:
                    cmd.run([self.appid])
        # make sure repository scheduler started
        scheduler_start_message = (
            "INFO:cubicweb.repository:starting repository scheduler with "
            "tasks: update_feeds, expire_dataimports"
        )
        self.assertIn(scheduler_start_message, log_cm.output)
        # and that scheduler's run method got called
        self.assertIn("boom", str(exc_cm.exception))
        patched_run.assert_called_once_with()
        # make sure repository's shutdown method got called
        repo_shutdown_message = "INFO:cubicweb.repository:shutting down repository"
        self.assertIn(repo_shutdown_message, log_cm.output)

    def test_source_sync(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity(
                "CWSource",
                name="success_feed",
                type="datafeed",
                parser="test_source_parser_success",
                url="ignored",
            )
            cnx.create_entity(
                "CWSource",
                name="fail_feed",
                type="datafeed",
                parser="test_source_parser_fail",
                url="ignored",
            )
            cnx.commit()

            cmd = SynchronizeSourceCommand(None)
            cmd.config.force = 1

            # Should sync all sources even if one failed
            with self.assertRaises(ExecutionError) as exc:
                cmd.run([self.appid])
            self.assertEqual(len(cnx.find("Card", title="success")), 1)
            self.assertEqual(len(cnx.find("Card", title="fail")), 0)
            self.assertEqual(str(exc.exception), "All sources where not synced")

            # call with named sources
            cmd.run([self.appid, "success_feed"])
            self.assertEqual(len(cnx.find("Card", title="success")), 2)

            with self.assertRaises(ExecutionError) as exc:
                cmd.run([self.appid, "fail_feed"])
            self.assertEqual(str(exc.exception), "All sources where not synced")
            self.assertEqual(len(cnx.find("Card", title="fail")), 0)

    def test_db_check_no_db(self):
        init_db_name = self.config.system_source_config["db-name"]
        self.config.system_source_config["db-name"] = "not existing db"
        try:
            with self.assertRaises(SystemExit) as ctx:
                repo_cnx(self.config)
            self.assertEqual(ctx.exception.code, 1)
        finally:
            self.config.system_source_config["db-name"] = init_db_name


if __name__ == "__main__":
    from unittest import main

    main()
