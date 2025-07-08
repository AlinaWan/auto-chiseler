name: 🐞 Bug Report
about: Report a problem or unexpected behavior in Pip Reroller
title: '[Bug] '
labels: bug
assignees: ''

body:
  - type: markdown
    attributes:
      value: |
        ## Bug Report

        Please fill out the following information to help us identify and fix the issue.

  - type: input
    id: description
    attributes:
      label: Bug Description
      placeholder: Describe the bug or issue you encountered in detail
      required: true

  - type: input
    id: steps
    attributes:
      label: Steps to Reproduce
      placeholder: List the steps to reproduce the bug
      required: true

  - type: input
    id: expected
    attributes:
      label: Expected Behavior
      placeholder: What you expected to happen
      required: true

  - type: input
    id: actual
    attributes:
      label: Actual Behavior
      placeholder: What actually happened
      required: true

  - type: input
    id: os_specs
    attributes:
      label: Operating System and Specs
      description: Please include your OS version and relevant hardware specs (CPU, GPU, RAM)
      placeholder: e.g. Windows 10 21H2, Intel i7-9700K, 16GB RAM, NVIDIA RTX 3080
      required: true

  - type: input
    id: average_ping
    attributes:
      label: Average Ping (ms)
      description: Provide your average network ping while using Pip Reroller
      placeholder: e.g. 45 ms
      required: true

  - type: input
    id: monitor_refresh_rate
    attributes:
      label: Monitor Refresh Rate (Hz)
      description: What is your monitor's refresh rate?
      placeholder: e.g. 60 Hz, 144 Hz
      required: true

  - type: input
    id: fps
    attributes:
      label: Average FPS (Frames Per Second)
      description: What FPS do you typically get when running Pip Reroller?
      placeholder: e.g. 60 FPS, 120 FPS
      required: true

  - type: textarea
    id: additional_info
    attributes:
      label: Additional Information
      description: Anything else that might help us debug the issue
      placeholder: Logs, screenshots, error messages, etc.
      required: false
