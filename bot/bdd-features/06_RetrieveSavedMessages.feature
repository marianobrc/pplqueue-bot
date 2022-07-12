Feature: Retrieve saved messages
    As a slack user
    I want the bot to show me my saved messages organized by priority
    So that I can check them now

  Scenario: Ask the bot to list all my saved messages
    Given that there are saved messages
    When I send a direct message to the bot
    And I use the words "list" or "list messages"
    Then the bot shows a list of messages ordered by priority and then by timestamp
    And each item of the list has the picture and name of the sender, a time reference like "x mins/hs/days ago", and a link to the message
    And each item of the list has an button / icon to remove it from the list

  Scenario: Ask the bot to pop the next message in the list
    Given that there are saved messages
    When I send a direct message to the bot
    And I use the words "next" or "next message"
    Then the bot shows the next, most prioritary message
    And it shows the picture and name of the sender, a time reference like "x mins/hs/days ago", and a link to the message
    And it shows a button or an icon to remove the message from the list
