---
title: "Secrets Management: Beyond Environment Variables"
date: "2021-03-23"
tags: ["Security", "DevSecOps", "Infrastructure", "Vault"]
summary: "Environment variables are not secure storage. We migrated from .env files to HashiCorp Vault for dynamic secrets injection."
status: "published"
---

"Where do I put the DB password?"

"Just put it in the `.env` file and don't commit it."

This advice is common, and it is dangerous. `.env` files get accidentally committed. They get pasted into Slack. They sit unencrypted on developer laptops.

As we move towards SOC2 compliance, "environment variables" are no longer an acceptable answer for secrets management.

## The Problem with Kubernetes Secrets

Even Kubernetes Secrets are just base64 encoded strings. Anyone with `kubectl get secrets` access can decode and read your production Stripe API keys.

We need:
1.  **Encryption at Rest:** Real encryption, not encoding.
2.  **Audit Logs:** Who accessed this secret and when?
3.  **Rotation:** The ability to change a password without redeploying the app.

## Adopting HashiCorp Vault

We chose Vault as our central secrets engine. It is complex to run, but the security guarantees are unmatched.

### The Sidecar Injection Pattern

Instead of the application reading from an environment variable, we use the Vault Agent Injector.

1.  A pod starts up.
2.  The Vault Agent sidecar authenticates with Vault using the Kubernetes Service Account (Identity).
3.  Vault checks the policy: "Does `service-account-checkout` have read access to `secret/checkout/db`?"
4.  If yes, the agent writes the secret to a shared memory volume at `/vault/secrets/config.json`.
5.  The application reads the config file on startup.

The application **never** sees the secret as an environment variable. If you run `env` inside the container, you see nothing.

## Dynamic Secrets

The killer feature is dynamic secrets.

For our Postgres database, the application doesn't have a static username/password.
When the app starts, Vault connects to Postgres, creates a *temporary* user with a 1-hour lease, and gives those credentials to the app.

If an attacker steals those credentials, they are useless after an hour. We can also revoke them instantly.

## Complexity Tax

Vault is not free. It is a distributed system that needs high availability (HA) storage (Consul). Running it is a full-time job.

But for a fintech or healthcare company, the cost of a leaked database credential is infinite. The operational tax of Vault is the price of sleeping at night.

## What I Would Do First

If you are just starting, do not boil the ocean. Start with a single critical secret and wire up the audit trail. Once you prove the pattern, move the rest.

The biggest cultural shift is getting engineers to stop treating secrets as configuration. Secrets are identity, and identity has to be managed like production data.
