Feature: Save messages for later
    As a slack user
    I want the bot to save messages
    So that I can review them later

  Scenario: Ask the bot to save a message in a channel
    Given that a message of my interested was written in a channel
    And the bot is in that channel
    And I am subscribed to the bot
    When I respond the message in a thread
    And I @mention the bot
    And I use the words "save message [label]"
    Then the bot saves a link to the message with a priority and optionally with a label (see SetPriorities feature)
    And answers with a message in teh same thread telling that a link to this message was saved

  Scenario: Ask the bot to save a message in a thread
    Given that there is a conversation of my interested in thread
    And the bot is in that channel
    And I am subscribed to the bot
    When I respond the message in a thread
    And I @mention the bot
    And I use the words "save thread"
    Then the bot saves a link to the head message of the thread with a priority and optionally with a label (see SetPriorities feature)
    And answers with a message in the same thread telling that a link to this thread was saved
