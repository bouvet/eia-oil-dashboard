QA Insight Template
QA in development teams

As a new QA in a team, or as a QA in an existing team, it is valuable to go through the team’s processes from time to time.
This insight template is intended for QA resources to reflect on what may be important when observing a team. Do not use this template as an interview template; instead, take the time to get a good overall understanding of how the team works.
The outcome of this insight should be documented in the QA strategy template (available on GitHub). This is to capture how the team works and also to get to know the team. It is important that everyone in the team has a holistic understanding of how the team works, which practices work well, and where there is room for improvement.
What is important to keep in mind is that not all teams work in the same way, and the goal is not that everyone should work in the same way. The purpose of this template is rather to identify where the pain points are and where adjustments can be made.
In this document, there are a number of questions that should be documented. The chapters are based on the model below.
1 Questions for QA in work processes

Spend some time observing how the team actually works before starting the documentation. Involve the whole team so that everyone actually has insight into how the team works in practice.
1.1 Process and workflow

    Which Agile methodology does the team use?
    Which tool is used to show how the team works?
    How is the work process documented today?
    What does the workflow look like, and which statuses are used?
    Why do they work this way today?
    Which processes work best today – and why?
    Which tool does the team use to show the progress of work tasks?
    What is the process for Epics and Features, if any?
    What does a typical sprint or work week look like for the team?
    How does the team prioritize tasks, and who is involved in the prioritization?
    How does the team break down tasks?
    How are user stories created?
    How are work items made ready for development?
    How does the team write acceptance criteria?
    What are the criteria for something being “ready” (Definition of Ready, DoR) for development?
    What does the team’s Definition of Done (DoD) look like?
    When does the team know that a work item is “Done”?
    How often are things released to the production environment?

1.2 Role distribution and collaboration

    How do developers, QA, designers, and the product owner collaborate in practice?
    Who makes decisions when unresolved issues arise?
    How does the team handle dependencies between teams and external stakeholders?
    Are there any defined role descriptions for the different roles in the team?

1.3 Planning and estimation

    How does the team estimate tasks, and how accurate is it today?
    Which tools does the team use for planning and follow-up?
    How does the team handle changes that come in the middle of a sprint?
    How do changes come into the team?
    How are bugs reported to the team?
    How does the team handle bugs – both urgent ones and those that remain unresolved?

1.4 Quality, testing, and delivery

    How does the team ensure quality throughout the development lifecycle?
    How is QA involved in the design, requirements, and planning phase?
    When and how do you define test scenarios?
    How do you ensure a shared understanding of requirements and acceptance criteria?
    When and how does the team test (manually, automated, continuously)?
    How are findings discovered along the way handled – do they stop development, or are they handled in parallel?
    How does the team share learning, improvements, and retrospective results?
    How do you evaluate delivery quality over time?

1.5 Deliveries and goal achievement

    How does the team measure progress and delivered value?
    How does the team know that what they are building is the right thing – and that it is actually being used?
    How does the team know that a delivery has achieved its goals (e.g. usage, quality, and business value)?
    How does the team handle deviations from the planned delivery (delays, changes, scope adjustments)?
    How often does the team deploy to production?
    What form of user acceptance does the team have today before and after production?

1.6 Communication and transparency

    How does the team keep each other updated on progress and challenges?
    How are users or customers involved in the development process?
    What types of meetings does the team have, how do they work in practice, and who should participate?
    What does a typical retrospective look like – and which actions does the team actually implement?
    How does the team share learning, improvements, and retrospective results?
    Is there psychological safety to speak up about errors or challenges – and how does the team handle challenging questions?
    How does the collaboration between the team and the product owner/customer work?
    How does the team communicate with stakeholders outside the team?

1.7 Security and robustness

    How does the team assess and safeguard security in the development process?
    How does the team ensure the security of the solution (e.g. regular threat modeling meetings)?
    How does the team work with logging, monitoring, and incident management?
    Which external monitoring/observability tools does the team use (e.g. Application Insights, Grafana, Datadog, Sentry, PagerDuty) that are not visible in the repository?
    How does the team work to avoid technical debt, and how does the team prioritize it?

1.8 Capacity, load, and pace

    How does the team assess its capacity from sprint to sprint?
    How does the team balance planned tasks against unforeseen events?
    Does the team experience time pressure, and how is it handled?
    How does collaboration with the customer work with regard to operational tasks?

1.9 Technical choices and architecture

    How does the team make decisions about technology and frameworks?
    How does the team ensure that the architecture is scalable and future-proof?
    How does the team handle legacy systems or older codebases?
    How are operational tasks and refactoring prioritized – and is the customer on board?

1.10 Challenges and improvements

    What are the biggest bottlenecks the team is experiencing today?
    Which processes work the worst, and why?
    If the team could change one thing in the process – what would it be?
    What do they want to achieve by making changes to the processes?
    Which improvements should be implemented?
    Which changes require little adjustment but have a large benefit?
    How can/is AI used, and which AI engine is used?

2 Questions for QA in build processes
2.1 Testing as part of the build process

    How much of the testing is automated, and which types of tests does the team have (unit tests, API tests, end-to-end tests, etc.)?
    Does the team run tests automatically on commit, PR, or before merge?
    What happens if a test fails in the pipeline – and how quickly is it followed up?
    Does the team actively use test coverage or other quality assurance measures?
    How can the team demonstrate the benefits of “fail fast” (for example through automated tests)?

2.2 Technical practices

    How does the team work with code reviews?
    How do the CI/CD pipeline and deployment process work?
    How does the team document, and how up to date is the documentation?

2.3 CI/CD and validation

    How are the tests integrated into the CI/CD pipeline?
    How often are the tests updated to reflect changes in the code or requirements – and who updates them?
    How does the team ensure that the pipeline is stable and provides reliable results?

2.4 Test environments and data

    How many different environments does the team have?
    When does the team test (who, what, and where)?
    How does the team handle test environments – are they stable, automated, or manual?
    How does the team use test data, and how does the team ensure that it is representative and up to date?
    How does the team assure the quality of APIs, integrations, and external dependencies?

2.5 Challenges and improvements

    Why has the team chosen to work this way?
    What challenges does the team currently have with regard to the build processes?
    What can the team improve?
    What do they want to achieve by making changes to the processes?
    Which improvements should be implemented?
    Which changes require little adjustment but have a large benefit?
    How can/is AI used, and which AI engine is used?

3 Questions for the Agile QA Quadrant
3.1 Create the team’s Agile QA Quadrant

The Testing Quadrant model divides different types of testing into four quadrants to help teams understand what is being tested, why, and when in an agile process. It also shows how tests support either the team or the product, and whether they have a more technical or business-oriented nature.
Use the model above as a starting point to map out how the team works in the different areas.
3.2 Challenges and improvements

    Which types of tests are used in the team?
    Who does what?
    Why has the team chosen to work this way?
    What challenges does the team currently have with regard to the different types of tests?
    What can the team improve?
    What do they want to achieve by making changes to the test methods?
    Which new tests should be implemented?
    Which changes require little adjustment but have a large benefit?
    Which improvements will take longer to implement but will have a large benefit?
    How can/is AI used, and which AI engine is used?

3.3 Manual testing and test management

    Does the team maintain manual test cases or test suites? If so, where are they stored (e.g. Azure Test Plans, TestRail, Zephyr Scale, Xray, spreadsheets, wiki)?
    How many manual test cases exist approximately, and who owns them?
    How often are manual tests executed (e.g. every sprint, before release, ad-hoc)?
    Are the manual test cases kept up to date when features change, or do they tend to go stale?
    Is there traceability between manual test cases and requirements or user stories?
    Are manual test results recorded and tracked over time, or executed without formal pass/fail logging?
    Which manual tests, if any, are candidates for automation? What is blocking that transition?
    Does the team do structured exploratory testing, or is exploratory testing informal and unrecorded?

4 Questions for the Test Pyramid
4.1 Create the team’s Test Pyramid

The test pyramid is a conceptual framework for software testing that emphasizes the proportion of different types of automated tests that should be used to create a balanced and effective test strategy.
The most effective test suites have a larger lower level than higher-level integration or end-to-end testing. This approach can lead to faster feedback on code changes, easier maintenance, and reduced costs. It also ensures that errors are discovered early, when they are cheaper and easier to fix.
Use the model above as a starting point to map out how the team works in the different layers of the pyramid. Feel free to include how much test coverage the team has at the different levels.
4.2 Challenges and improvements

    How does the team perform with regard to the model above, and what is the test coverage at the different levels, if it is used?
    Who does what?
    Why has the team chosen to work this way?
    What challenges does the team currently have with regard to these tests?
    What can the team improve?
    What do they want to achieve by making changes to the test methods?
    Which improvements should be implemented?
    Which changes require little adjustment but have a large benefit?
    Which improvements will take longer to implement but will have a large benefit?
    Which tools are used, and are they approved by the customer?
    What authentication problems (if any) does the team have when it comes to tests – and at which level are they (e.g. unit and/or integration)?
    How can/is AI used, and which AI engine is used?
