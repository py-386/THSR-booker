from typing import Optional
from pydantic import BaseModel, ConfigDict

from selenium.webdriver.remote.webelement import WebElement


class TrainInfo(BaseModel):
    depart_time: str
    arrival_time: str
    duration: str
    train_code: str
    radio_box: WebElement

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserRequirements(BaseModel):
    departure_station: str
    destination_station: str
    date: str
    time: str


class UserInfo(BaseModel):
    id: Optional[str]
    phone_number: Optional[str]
    e_mail: Optional[str]
