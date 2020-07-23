from aiogram import executor, Dispatcher

import fastdb
import globalset
import misc
from misc import dp
import handlers
if __name__ == "__main__":
    # globalset.refresh_positions()
    fastdb.refresh_all_fastdb()
    executor.start_polling(dp, skip_updates=True)

