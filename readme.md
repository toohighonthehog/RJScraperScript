# Prereqs

#apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

# https://stackoverflow.com/questions/67298635/request-html-render-working-on-windows-but-not-on-ubuntu

# Mount into WSL

# sudo mount -t cifs -o username=xadmin //192.168.192.35/multimedia /mnt/multimedia

# sudo mount -t cifs -o username=xadmin //192.168.192.35/vmwareshares /mnt/vmwareshares

# Useful

# ffmpeg -i <source> -vn -acodec copy <destination>.aac

# https://colab.research.google.com/github/richardjj27/WhisperWithVAD

To do:

## add a rerun option + re-get json - done by creating a move down a level function

## how about putting all the jsons in a central folder too? - done

## send results to a database - done

## logging for output - done

## add subtitle available attribute - done

## get date working in metadata

## actress to actor - done

## check if incumbent subs exist, so may the subs_avaiable setting True regardless of SC. - done

## if it can't be found, don't move it - just skip

## multiple file extensions? (MP4, MKV, AVI)

## If it doesn't exist, create an actor row. Needs Testing - seems to be working - test a bit more.

## Fix/Rename the 'moved' subtitle file. Exclude TARGET_LANGUAGE or make the filename fix (-) only work with the first set of letters and numbers. Right now, it is stripping the target language so be careful. - done? if it works, code can be easier.

## Add a 'file to the right place' option. i.e. a source and destination constant. - need to test

## Check TARGET_DIRECTORY exists

#3 Add some more checks, especially things which can go wrong destructively. examples?

## Probably need to do a bit of tidying up with filename fixing now that we have the more advanced fix_file_code function.

## Add a switch on whether to run the 'move down level' function first. Makes it eaiser than remarking out.

## Check subtitle flag gets checked when going to a different target.

## Turn the whole thing into a module and have a few wrapper scripts.

#? and some logic to check we're not nesting deeper and deeper

## Make existing subtitles rename to match the main file. Maybe it already works.

## Add an affirmative statement that there has been a single, good match.

## Add a recheck for failed downloads (i.e. try 3 times then give a warning). Make it more resilient and try to look up less. or put them into a wrapper function with resilience added.

## Add link to results. As a table (as they can give multiple results?) or just the first result?

## Semi-modularize (so that the functions run when imported) - started

#+ Variables in functions should start with 'f*' for attributes and 'p*' for internal variables. Also tidy up everything else.

## each function should return something even if just True/False - add something useful

## how do we get the logging and databases into the functions?

# A bit more resilience for failed lookups. We fail non-destructively now but it'd be nice to have some retries for URL lookups etc.

## we need to get f_metadata_url written to JSON.

## Make the 'get a confirmed name' process faster and more consistent. Seems to not do the 6 thing when running on the fix_flat.

## Send verbose logs to a file

## Reliable recovery from failure (i.e. what to do with a half done file?) make the move the last step?

## Create a stub record as early as possible?

## Then populate at the end.

## or do the invasive tasks last

## Need to make faster.

## Differentiate between lookup failure and an affirmative null result.

## Log file to timestamped filename

## if a strict <filename>-<target language> file doesn't already exist copy the largest srt to make it.

## Now retrieves subtitles from a local store if they exist and appends a (LR) suffix.

## Removed unused variables (especially from functions)

## Add a move/copy option to the below, with MOVE as default to 'move_files_by_extension' function. Rename it too.

## shutil.move instead of os.rename

## Standardize function argument order.

## Check to see what is searched for matches what is found HUNT014 > HUNT146, for example

## Move the functions into processed order.

# Standardise on SOURCE (base) and TARGET (destination)

# Standardise DIRECTORY and PATH.

# Standardise FILENAME in the functions

## Subtitle status. Simplify and just do a one time check in ...

## 0 - missing

## 5 - exist but don't match target language (general)

## 6 - exist but don't match target language (whisper)

## 9 - exist and match target language

## Add an entry for unknown files which strictly match the \*-nnn format

## Do a cleanup of items which can't be found. Most of the metadata will be blank for these.

#+ Test whisper respository code.

# add find duplicate check

# added date will be for the whole batch

# if we're adding something which already has a record with the same batch date/time, carry on as normal but with a warning.

# this will involve some queries of live data. where else do we need to use this?

# Create a 'scan for issues' option.

# Does a file exist for each record?

# Create a 'to be rescanned' flag.

# Tidy up the dedup script. Make it a bit faster.

# Audit the data which is updated on a rescan.

# The '5' value to generate the MP3 runner should clear after the .sh file is created.

# Check that the URL is correct DVMM-003 and returning DVMM-033 for some reason.

Done:
