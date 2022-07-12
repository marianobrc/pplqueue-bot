Feature: Remove the bot from a Slack channel
    As a slack user
    I want to remove the bot from a Slack channel
    So that it is not used in that channel anymore

  Scenario: Remove the bot from a Slack channel
    Given that the bot app is a member of a Slack channel
    When I remove the bot from the channel
    Then the bot is no longer available in that channel
    And the bot doesn't react to messages written in that channel anymore

  Scenario: Remove the bot from a Slack workspace
    Given that the bot app is already installed in a workspace
    When I remove the bot app from the workspace
    Then app in removed
    And all the related data is deleted
