Feature: Set messages priority
    As a slack user
    I want to assign different priorities at channel-level, user-level,  or message-level
    So I can order and retrieve messages by priority later

  Scenario: Save a message with a selected priority
    Given that the bot is installed on this workspace
    When I ask the bot to save a message or a thread
    And I use the words "priority <highest|high|medium|low|lowest>"
    Then the message is saved with the selected priority

  Scenario: Set a priority at channel-level
    Given that the bot is installed on this workspace
    When I @mention or DM the bot and I #mention a channel
    And I use the words "set priority <highest|high|medium|low|lowest>"
    Then the bot sets the channel-level priority to the selected one
    And all the upcoming messages in that channel will have set this channel-level priority

  Scenario: Set a priority at user-level
    Given that the bot is installed on this workspace
    When I @mention or DM the bot and I @mention another user
    And I use the words "set priority <highest|high|medium|low|lowest>"
    Then the bot sets the user-level priority to the selected one
    And the user-level priority overrides the channel-level priority if set
    And all the upcoming messages from that user will have set this user-level priority

  Scenario: Set a priority at message-level
    Given that the bot is installed on this workspace
    When I ask the bot to save a message
    And I use the words "set priority <highest|high|medium|low|lowest>"
    Then the bot saves the message with the selected priority
    And the message-level priority overrides any other priority at channel-level or user level if set

  Scenario: Save a message with the Default priority
    Given that the bot is installed on this workspace
    And no priorities are set at any level
    When I ask the bot to save a message or a thread
    And I don't specify a message priority
    Then the message is saved with the <medium> priority


