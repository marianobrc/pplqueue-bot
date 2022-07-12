
Feature: Add the bot to a slack channel
    As a slack user
    I want to add the bot in a channel
    So that I can use the bot

  Scenario: Add the bot to the workspace the first time
    Given that the bot app is not installed in this workspace
    When I got to the Slack Apps Store
    And I select to install the Bot
    Then the bot is added to the workspace and it joins the current channel

  Scenario: Add the bot to a new channel
    Given that the bot app is already installed in this workspace
    When I invite the bot to a new channel
    Then the bot joins the current channel
    And the bot sends a hello message with usage instructions