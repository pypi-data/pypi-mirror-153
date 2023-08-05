import asyncio
import selenium.common.exceptions
from main import main, logger

try:
    asyncio.new_event_loop().run_until_complete(main())
except (KeyboardInterrupt, selenium.common.exceptions.NoSuchWindowException):
    pass
except selenium.common.exceptions.WebDriverException as err:
    logger.info(err)
logger.info("End of program.")
