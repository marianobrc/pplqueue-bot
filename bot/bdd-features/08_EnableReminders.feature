Feature: Enable reminders
    As a slack user
    I want to get remainders of saved messages
    So I don't forget to review messages

  Scenario: Set a remainder on a specific message
    Given that the bot is installed on this workspace
    And the bot jas joined the channel where the target message or thread lives
    When I ask the bot to save the target message or thread
    And I add the words "reminder in <3m|3h|3d>"
    Then the message is saved with the selected priority and the specified reminder time
    And the bot will send me a direct message at the set time to remind me about that message

  Scenario: Set a daily remainder about saved messages
    Given that the bot is installed on this workspace
    When I @mention or DM the bot
    And I use the words "reminder <daily> at <hh::mm>"
    Then the bot will send me a direct message at the set time
    And it will show me my list of saved messages

