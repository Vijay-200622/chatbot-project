"""Tests for topic filter functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.services.topic_filter import (
    detect_topic,
    is_within_syllabus,
    get_out_of_syllabus_message,
    get_all_topic_names,
)


def test_detect_photosynthesis():
    topic = detect_topic("bhaiya photosynthesis samajh nahi aaya")
    assert topic is not None
    assert "Photosynthesis" in topic["topic"] or "Life Processes" in topic["topic"]


def test_detect_newton():
    topic = detect_topic("Newton's law of motion explain karo")
    assert topic is not None
    assert "Newton" in topic["topic"] or "Motion" in topic["topic"] or "Force" in topic["chapter"]


def test_detect_electricity():
    topic = detect_topic("electricity and current kya hai")
    assert topic is not None
    assert "Electricity" in topic["topic"]


def test_out_of_syllabus():
    within, topic = is_within_syllabus("explain blockchain cryptocurrency and NFT trading")
    # This should not match any NCERT topic
    assert topic is None or within is False


def test_within_syllabus():
    within, topic = is_within_syllabus("what is photosynthesis chlorophyll sunlight")
    assert within is True
    assert topic is not None


def test_get_all_topics():
    topics = get_all_topic_names()
    assert len(topics) > 30  # We have 55+ topics
    assert "Electricity" in topics


def test_out_of_syllabus_message():
    msg = get_out_of_syllabus_message()
    assert "NCERT" in msg
    assert "class 9-10" in msg


if __name__ == "__main__":
    test_detect_photosynthesis()
    test_detect_newton()
    test_detect_electricity()
    test_out_of_syllabus()
    test_within_syllabus()
    test_get_all_topics()
    test_out_of_syllabus_message()
    print("✅ All topic filter tests passed!")
