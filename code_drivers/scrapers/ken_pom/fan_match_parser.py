import datetime
import logging
import os
import sys
import traceback
from concurrent import futures

from sqlalchemy import create_engine

from lib.dao.fan_match_dao import FanMatchDAO
from lib.domain.base import Base
from lib.soup.fan_match_soup import FanMatchSoup
from lib.utils.env import Env
from lib.utils.fs import FS

started = []
ended = []

def run(date, fan_match_soup, fan_match_dao):
    process = date.strftime("%Y-%m-%d %H:%M:%S.%f %z")

    print(f"{process} starting...")
    started.append(process)

    for prediction in fan_match_soup.run(date):
        fan_match_dao.save_or_update(prediction)

    fan_match_dao.commit()
    ended.append(process)
    print(f"{process} finished...")


def main():
    engine = create_engine(Env.database_url())

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    fan_match_dao = FanMatchDAO(engine)

    with futures.ThreadPoolExecutor() as executor:
        threads = []

        for entry in os.listdir("./output/html"):
            with open(os.path.join("./output/html", entry), "r") as f:
                [year, month, day] = entry.replace(".html", "").split("-")

                date = datetime.datetime(int(year), int(month), int(day))

                threads.append(
                    executor.submit(
                        run,
                        date=date,
                        fan_match_soup=FanMatchSoup(f.read()),
                        fan_match_dao=FanMatchDAO(engine),
                    )
                )

        futures.wait(threads)

    print("started:", len(started))
    print("ended:", len(ended))


if __name__ == "__main__":
    main()
