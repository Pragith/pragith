---
title: "Kubernetes Networking: Why My Service Can't Talk to Yours"
date: "2021-04-09"
tags: ["Kubernetes", "Networking", "Istio", "Service Mesh"]
summary: "We spent three days debugging a 503 error because we misunderstood how Kubernetes services resolve DNS. Here is a deep dive into ClusterIP, NodePort, and Ingress."
status: "published"
---

Kubernetes makes deploying containers easy. It makes networking containers hard.

Last week, we deployed a new microservice (`recommendation-engine`) that needed to talk to our legacy monolith (`core-api`).

The result? `Connection Refused`.

It turns out that "Service Discovery" is not magic. It relies on a chain of DNS resolvers (CoreDNS), iptables rules (kube-proxy), and network policies (Calico) that must all align perfectly.

## The DNS Resolution Chain

When a pod in namespace `data` tries to call `http://core-api`, it fails. Why?

Kubernetes DNS is namespaced. The full FQDN is `core-api.default.svc.cluster.local`.

If your application code just hardcodes `core-api`, it relies on the `/etc/resolv.conf` search path in the container. We found that our Alpine-based images had a different `ndots` configuration than our Debian-based images, causing lookup failures for short names.

## The Ingress Confusion

We also confused **Service** (internal) with **Ingress** (external).

*   **ClusterIP:** The default. Only reachable from within the cluster.
*   **NodePort:** Opens a port on every worker node. Good for debugging, bad for security.
*   **LoadBalancer:** Provisions a cloud LB (AWS ALB / GCP LB). Expensive.
*   **Ingress:** A smart router (Nginx / Traefik / Istio) that sits at the edge and routes HTTP traffic based on hostnames.

We were trying to use an Ingress to route internal traffic between services. This is an anti-pattern. Ingress is for traffic entering the cluster from the internet. East-West traffic (service-to-service) should happen via ClusterIP DNS.

## Enter the Service Mesh (Istio)

To solve visibility into these failures, we are piloting Istio.

Istio injects a sidecar proxy (Envoy) into every pod. All network traffic goes through the proxy.

This gives us:
1.  **mTLS:** Mutual TLS encryption between all services by default.
2.  **Traffic Splitting:** Send 1% of traffic to v2, 99% to v1.
3.  **Observability:** We can see exactly which service is returning 500s on the service graph.

The complexity of Istio is high, but the visibility it provides into the black box of Kubernetes networking is worth it.

## What I Document Now

After this incident, we wrote a one-page "service discovery primer" for every engineer. It includes the DNS format, the service types, and the default search paths for each base image.

Networking bugs are rarely a single issue. They are a chain of assumptions. The only way to break that chain is to make the assumptions explicit.
