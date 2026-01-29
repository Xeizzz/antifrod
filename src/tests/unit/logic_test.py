import pytest
from datetime import date
from unittest.mock import patch
from app.service.antifraud_service import AntifraudService

def test_calculate_age():

        assert AntifraudService.calculate_age("28.01.2000") == 26

        assert AntifraudService.calculate_age("12.01.2010") == 16

        assert AntifraudService.calculate_age("01.01.2008") == 18

def test_is_adult():

        assert AntifraudService.is_adult("28.01.2002") is True

        assert AntifraudService.is_adult("03.01.2012") is False