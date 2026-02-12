---
title: "Stop Copy-Pasting Terraform: The Module Monolith"
date: "2021-08-30"
tags: ["Terraform", "Infrastructure as Code", "DevOps", "Refactoring"]
summary: "Our Terraform codebase grew from a manageable set of files to a sprawling mess of copy-pasted resources. We refactored it into reusable modules, but found new trap doors."
status: "published"
---

Infrastructure as Code (IaC) starts simple. You define an S3 bucket resource. Then another. Then another.

Fast forward 18 months, and our Terraform repository has 50,000 lines of HCL (HashiCorp Configuration Language). We have 20 different S3 buckets defined, and half of them have slightly different encryption settings because someone forgot to copy the latest configuration.

We declared "Bankruptcy" on our root module and started refactoring into a modular architecture.

## The Module Strategy

We created a library of "Approved Modules":
*   `modules/s3-secure-bucket`
*   `modules/rds-postgres-production`
*   `modules/gke-standard-cluster`

These modules abstract away the complexity. They enforce:
*   **Best Practices:** Enforced encryption, logging enabled, public access blocks.
*   **Tagging:** Mandatory cost center tags.
*   **Naming Conventions:** Automatic prefixing.

Now, a developer just instantiates the module:

```hcl
module "user_uploads" {
  source      = "./modules/s3-secure-bucket"
  name        = "user-uploads"
  environment = "prod"
}
```

## The Versioning Trap

The immediate problem we hit was versioning.

If we change the `s3-secure-bucket` module, does it update all 50 buckets immediately? That is terrifying. A bad change could destroy state across the entire org.

We moved to **Remote Modules with Git Tags**.

```hcl
source = "git::https://github.com/org/infra-modules.git//s3-secure-bucket?ref=v1.2.0"
```

This acts like a software dependency. We can release `v1.3.0` of the bucket module, and teams can upgrade at their own pace. It prevents the "monolith" problem where a single `terraform apply` takes 45 minutes and touches every resource in the account.

## What We Enforced After the Refactor

Every module now has a README with inputs, outputs, and examples. If you cannot explain a module in one page, it is too complex.

We also added CI checks that prevent raw resources from being declared outside approved modules. It feels strict, but it forces reuse and keeps the codebase sane.

## Conclusion

DRY (Don't Repeat Yourself) applies to infrastructure just as much as application code. But unlike code, refactoring stateful infrastructure is dangerous. Plan carefully.
