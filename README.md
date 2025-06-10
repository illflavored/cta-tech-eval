
# Morgan Sveen CTA Tech Eval Project

This is a technical evauluation project that contains a simple FastAPI python application built with Docker and hosted on GCP's Cloud Run. There is an API endpoint that returns a formatted version of the National League standings in JSON.

Application is live at https://morgan-cta-eval-751310237922.us-east1.run.app/
### Docs
https://morgan-cta-eval-751310237922.us-east1.run.app/docs

### Example
https://morgan-cta-eval-751310237922.us-east1.run.app/docs#/default/get_standings_standings_get

```{
  "standings": [
    {
      "team": "New York Mets",
      "wins": 42,
      "losses": 24,
      "pct": ".636"
    },
    {
      "team": "Philadelphia Phillies",
      "wins": 38,
      "losses": 28,
      "pct": ".576"
    },
    ...
```

## Tech Stack

FastAPI, Python 3.13.4, Uvicorn, Docker, Google Container Registry, Google Cloud Run


## GitHub Actions Pipeline

To deploy this project, push to the main branch of the repository. GitHub Actions will execute lint, build, push, and deploy actions.

- Linting is performed by flake8 and will fail the build if rules are violated.
- Application is built using Dockerfile in the root directory
- Build artifact is a Docker image pushed to Google Container Registry (GCR)
- Deployment is to a Google Cloud Run instance

## Explanation of GitHub Secrets and Security

This project uses two secrets to securely connect GitHub Acations to the GCP project.

`GCP_PROJECT_ID` - Obfuscates the project ID

`GCP_SERVICE_ACCOUNT_KEY` - Contains the GCP Service Key

Since this is a public GitHub repository, we need to ensure that we can perform our Docker Push and Cloud Run deploy actions. We are using GitHub Repository Secrets which are not exposed in Actions logs and only accessible by repository admins. Anyone forking the repo will not have access.

The `GCP_SERVICE_ACCOUNT_KEY` is a JSON key created in the Google Cloud Console. A new service account was created and granted the roles that allow pushing a Docker image to the GCR and the publish to the Cloud Run instance.

### Additional Security Considerations
Given additional time there are several items that could be considered for hardening of the application including but not limited to:

- Consideration of disabling GitHub Actions for forks
- Making the repository private, or limiting access to actions that perform publish or deploy actions
- Scrutiny of IAM roles in GCP to adhere to least privilege
- Implementing authentication and authorization of the API

## Notes regarding multiple environments

A punch list of actions for extending the application to multiple environments

- Add desired New Environments in GitHub Repository Settings - Development / Staging / Production
- Scope Environment Variables to each Environment. You will likely have different GCP projects which would require different GCP Account Keys.
- Ensure Docker tag rules reflect where the build came from. A pattern to distinguish a build intended for development, vs. a build ready for production.
- Set up rules for actions and branches. A simple methodology would be to deploy to production off main, and to Development on not main. Additional rules could consist of additional code metrics while developing, or post deployment validation such as performance metrics or uptime on production.

## Open Questions / Assumptions / Trade-offs

- There is no monitoring or alerting enabled, which ties in to performance and cost considerations on the hosting side. If we have a lot of traffic or an outage, we'll probably only know about this after the fact.
- I implemented IAM roles for the service account to use Admin roles which is likely overkill. This was a tradeoff made due to my unfamiliarity of in depth GCP IAM roles and limited time for this evaluation.
- I'm using bleeding edge stable python (v3.13.4) which could potentially have negative consequences if there are other libraries needed for this application.
- Using `runs-on: ubuntu-latest` to execute GitHub actions isn't always ideal as `latest` isn't a version. Not pinning a version could break actions.
- Additional config options could be parameterized using GitHub Secrets (GCP region, GAR Region)
- Using the cloud generated DNS is not always ideal