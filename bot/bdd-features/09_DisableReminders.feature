Feature: Disable reminders
    As a slack user
    I want to disable remainders of saved messages
    So I don't get too many notifications

  Scenario: List remainders
    Given that the daily remainders are enabled
    When I @mention or DM the bot
    And I use the words "reminder list"
    Then the bot will show a list of all the enabled reminders
    And each item of the list has: <reminder_id>, <reminder_label>, <type: daily or message>, [linked message]

  Scenario: Disable remainders
    Given that  there is a reminder enabled for a message
    When I @mention or DM the bot
    And I use the words "disable reminder <reminder_id>"
    Then the selected remainder is disabled
    And the bot sends a message telling that the selected remainder is now disabled

  Scenario: Disable daily remainders about saved messages
    Given that the daily remainders are enabled
    When I @mention or DM the bot
    And I use the words "disable daily reminder"
    Then the daily remainders are disabled
    And the bot sends a message telling that the daily remainder is now disabled
