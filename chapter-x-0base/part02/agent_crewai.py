import os
from crewai import Agent, Task, Crew, Process

os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
os.environ["OPENAI_API_KEY"] = "EMPTY"
os.environ["OPENAI_MODEL_NAME"] = "openai/qwen3"

class DevelopmentCrew:
    def __init__(self, development_description, testing_description):
        # 定义程序员智能体
        self.programmer = Agent(
            role="资深程序员",
            goal="编写高质量、可维护的代码，实现功能需求",
            backstory="你是一位经验丰富的程序员，精通多种编程语言和设计模式。" +
                     "你注重代码质量，善于编写清晰、高效的代码，并且有很强的逻辑思维能力。",
            verbose=True,
            max_execution_time=300
        )

        # 定义测试工程师智能体
        self.qa_engineer = Agent(
            role="测试工程师",
            goal="确保代码质量，发现并报告缺陷，验证功能完整性",
            backstory="你是一位严谨的测试工程师，对细节极其敏感。" +
                     "你擅长设计测试用例，能够发现各种边界条件和潜在问题，" +
                     "确保交付的代码达到高质量标准。",
            verbose=True,
            max_execution_time=300
        )

        # 定义开发任务
        self.development_task = Task(
            description=development_description,
            agent=self.programmer,
            expected_output="完整的Python代码实现，包含所有要求的功能和必要的注释"
        )

        # 定义测试任务
        self.testing_task = Task(
            description=testing_description,
            agent=self.qa_engineer,
            expected_output="详细的测试报告，包含测试用例、发现的问题和改进建议",
            context=[self.development_task]
        )

    # 创建并运行开发团队
    def invoke(self):
        dev_crew = Crew(
            agents=[self.programmer, self.qa_engineer],
            tasks=[self.development_task, self.testing_task],
            process=Process.sequential,
            verbose=True
        )

        print("开始软件开发流程...")
        print("第一阶段：程序员进行功能开发")
        print("第二阶段：测试工程师进行质量验证")
        result = dev_crew.kickoff()
        print("\n开发流程完成，最终结果:")
        print(result)
        return result.raw


if __name__ == "__main__":
    # 从主函数传入任务描述
    dev_description = """开发一个用户管理系统，包含以下功能：
    1. 用户注册（用户名、邮箱、密码）
    2. 用户登录验证
    3. 用户信息查询
    4. 密码重置功能
    请使用Python编写清晰的代码，包含必要的注释和错误处理。"""
    
    test_description = """对开发的用户管理系统进行全面测试：
    1. 设计测试用例覆盖正常流程和异常情况
    2. 进行边界值测试和错误处理测试
    3. 验证所有功能是否符合需求
    4. 提供详细的测试报告和改进建议"""
    
    dev_crew = DevelopmentCrew(dev_description, test_description)
    dev_crew.invoke()