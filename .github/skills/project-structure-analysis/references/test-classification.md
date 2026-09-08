# Test Classification Rules

Reference for classifying tests by scope and layer during project structure analysis. Apply these rules to every test file found — **classify by what the test actually does, not by the folder it lives in**.

---

## Primary Classification: Scope and Assertions

| Layer | Definition | Examples |
|---|---|---|
| **Unit** | Tests a single function, class, or module in isolation. All dependencies are mocked or stubbed. No I/O, no network, no DB. | `[Fact]`/`[Theory]` in xUnit, `it()`/`test()` in Jest with mocked imports, `@Test` in JUnit with Mockito |
| **Integration** | Tests multiple real components together. May hit a real (or in-memory) database, file system, or internal service — but not external APIs. | ASP.NET Core `WebApplicationFactory`, Spring `@SpringBootTest`, pytest with a real DB |
| **API / Contract** | Calls HTTP endpoints directly and asserts on response status/body/headers. No browser. No UI interaction. | `cy.request()` in Cypress, `supertest` in Node.js, `HttpClient` in .NET, REST Assured in Java |
| **Component** | Renders an isolated UI component and asserts on its output or behavior. No routing, no real API calls. | React Testing Library `render()`, Vue Test Utils `mount()`, Angular `TestBed` |
| **E2E** | Exercises the full stack through a real browser or client UI. Simulates user interactions end-to-end. | Cypress `cy.visit()` + `cy.click()`, Playwright `page.goto()`, Selenium WebDriver |
| **Performance** | Measures response time, throughput, or load behavior under simulated traffic. | k6, JMeter, Locust, Artillery, Gatling |
| **Security** | Automated security scanning, dependency vulnerability checks, SAST/DAST. | OWASP ZAP, Snyk, Semgrep, `dotnet-retire` |
| **Accessibility** | Automated checks for WCAG compliance or accessibility violations in rendered UI. | axe-core, Lighthouse, `@axe-core/playwright` |

---

## Distinguishing API Tests from E2E Tests

This is the most common misclassification. A test in a `cypress/` or `e2e/` folder is **not automatically an E2E test**.

| Signal | Classification |
|---|---|
| Uses `cy.visit()` AND `cy.click()` / `cy.type()` / `cy.get()` to interact with the UI | E2E |
| Uses only `cy.request()` to call endpoints, no browser interaction | API |
| Uses a browser but only asserts on network responses (no DOM assertions) | API |
| Starts a browser, navigates to a URL, and asserts on visible page content | E2E |
| Uses `supertest`, `axios`, `fetch`, `HttpClient` against a running server | API |

**When a folder contains a mix:** count and classify each file individually.

---

## Identifying Stale / Inactive Tests

A test is **stale** if it meets any of these conditions:

- All test methods are commented out
- The file has a `[Skip]`, `@Ignore`, `@pytest.mark.skip`, `xit(`, `xdescribe(`, or `test.skip(` annotation on every test
- The test project targets a deprecated component (e.g. an old Azure Functions project that is no longer deployed)
- The test file has no test declarations at all (abstract base class only, no `[Fact]`/`it()` blocks)

Record stale tests in a separate **Stale / Commented-Out / Skipped** table — do not include them in active test counts.

---

## Counting Rules

- **All counts must be exact integers.** Never approximate.
- Count **test cases**, not test files, as the primary metric.
- For parameterized tests, count each data row as one test case:
  - `[Theory]` with 3 `[InlineData]` rows = 3 test cases
  - `it.each([...])` with 4 rows = 4 test cases
  - `@pytest.mark.parametrize` with 5 values = 5 test cases
- For `describe` blocks: count the inner `it()`/`test()` calls, not the `describe` itself.
- If a test file is impossible to count accurately without executing it (e.g. dynamically generated tests), note this explicitly as an assumption.

---

## Mock and Test Infrastructure

Do not classify mock/helper files as tests. Identify them separately:

- Mock classes or modules (e.g. `MockGraphHelper`, `MockTokenService`, `jest.mock(...)` at module level)
- Test factories or builders
- Shared fixtures and test data files
- Custom render wrappers (e.g. a `renderWithProviders()` helper)
- Auth helpers that bypass real SSO for testing

Record these under **Mock / Test Infrastructure** — they are QA-relevant but not test cases.

---

## Untested Areas

After classifying all tests, identify what is **not** covered:

- Controllers / route handlers with no test files
- Service classes with no unit tests
- API client / service layer on the frontend with no component or unit tests
- Page-level components with no tests
- Utility modules with no tests
- Reducers / state machines not covered by state logic tests

For each untested area, assign a risk rating:

| Risk | Meaning |
|---|---|
| **High** | Core business logic, auth flows, data mutation, or error handling paths |
| **Medium** | Presentation logic, routing, or state management |
| **Low** | Static configuration, pure display components with no conditional logic |
