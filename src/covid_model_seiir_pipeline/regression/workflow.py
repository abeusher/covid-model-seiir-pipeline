from typing import Dict
import shutil

from jobmon.client.swarm.executors.base import ExecutorParameters

from covid_model_seiir_pipeline.workflow_template import TaskTemplate, WorkflowTemplate


class RegressionWorkflow(WorkflowTemplate):

    @property
    def workflow_name_template(self) -> str:
        return 'seiir-regression-{version}'

    def build_task_templates(self, task_specifications: Dict[str, ExecutorParameters]):
        return {
            'regression': TaskTemplate(
                task_name_template="beta_regression_draw_{draw_id}",
                command_template=(
                        f"{shutil.which('beta_regression')} " +
                        "--draw-id {draw_id} " +
                        "--regression-version {regression_version} "
                ),
                params=task_specifications['regression']
            )
        }

    def attach_tasks(self, n_draws: int):
        regression_template = self.task_templates['regression']
        for draw_id in range(n_draws):
            task = regression_template.get_task(
                regression_version=self.version,
                draw_id=draw_id
            )
            self.workflow.add_task(task)
