import getopt
import os
import subprocess
import sys
import requests


# Todo [•] Create custom headers
# Todo [done] Create custom path for saving the files
# Todo [•] Create custom proxy
# Todo [•] Create platform independence
# Todo [done] Create fetch domain of chunks if not provided

def download_m3u8(path):
    print("Connecting to :" + path)
    print("...")
    try:
        response = requests.get(path)
        m3u8_file = str(response.content, 'utf-8')
        if m3u8_file is None or m3u8_file == "":
            print("File not found or link expired")
            return False
        f = open("temp.m3u8", 'w')
        f.write(m3u8_file)
        f.close()
        return True
    except Exception as e:
        print("Sorry the file couldn't be downloaded")
        print("Error: " + str(e))
        return False


def fetch_m3u8(path, base_link, output_dir, filename):
    if output_dir != "" and output_dir is not None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    if base_link is not "":
        if base_link[-1] == "/":
            base_link = base_link[:-1]

    # network request
    if "http" in path:
        result = download_m3u8(path)
        if result:
            f = open('temp.m3u8', 'r')
            links = []
            for row in f:
                if row.startswith("#"):
                    continue
                if not row.startswith("http"):
                    protocol = path.split("//")[0]
                    domain = path.split("//")[1].split("/")[0]
                    if row.startswith("/"):
                        links.append(protocol + "//" + domain + row[:-1])
                    else:
                        links.append(protocol + "//" + domain + "/" + row[:-1])
                else:
                    links.append(row[:-1])
            f.close()
            chunk_num = 0
            error_flag = 0
            subprocess.call('rm -rf temp_chunks', shell=True)
            subprocess.call('mkdir temp_chunks', shell=True)
            print("There are total of " + str(
                len(links)) + " chunks to download. Sit back and grab a coffee if you may like :)")
            for row in links:
                try:
                    proc = subprocess.Popen("wget '" + row[:-1] + "' -O temp_chunks/'" + str(chunk_num) + ".mp4' ",
                                            stdout=subprocess.PIPE, shell=True)
                    proc.wait()
                    (stdout, stderr) = proc.communicate()
                    if proc.returncode != 0:
                        print(str(stdout, 'utf-8'))
                        error_flag = 1
                        print("Couldn't Download----------->\n")
                        print("An error occurred while getting " + row[:-1])
                        break
                    else:
                        print(str(stdout, 'utf-8'))
                    chunk_num += 1
                except Exception as e:
                    print("An error occurred while getting " + row[:-1])
                    print(e)
                    error_flag = 1
                    subprocess.call("rm -rf temp_chunks", shell=True)
                    break
            if error_flag == 0:
                if output_dir is "":
                    if filename == "":
                        save_file = open('file.mp4', 'ab')
                    else:
                        save_file = open(filename, 'ab')
                else:
                    if filename == "":
                        if str(output_dir).endswith("/"):
                            save_file = open(output_dir + "file.mp4", 'ab')
                        else:
                            save_file = open(output_dir + "/file.mp4", 'ab')
                    else:
                        if str(output_dir).endswith("/"):
                            save_file = open(output_dir + filename, 'ab')
                        else:
                            save_file = open(output_dir + "/" + filename, 'ab')

                for i in range(0, len(links)):
                    f = open('temp_chunks/' + str(i) + ".mp4", 'rb')
                    save_file.write(f.read())
                    f.close()
                save_file.close()
                print("Done Mixin!")
                subprocess.call("rm -rf temp_chunks", shell=True)
                print("Success!")
    # system request
    else:
        f = open(path, 'r')
        links = []
        for row in f:
            if row.startswith("#"):
                continue
            if not row.startswith("http"):
                if row.startswith("/"):
                    links.append(base_link + row[:-1])
                else:
                    links.append(base_link + "/" + row[:-1])
            else:
                links.append(row[:-1])
        f.close()
        chunk_num = 0
        error_flag = 0
        subprocess.call('rm -rf temp_chunks', shell=True)
        subprocess.call('mkdir temp_chunks', shell=True)
        print("There are total of " + str(
            len(links)) + " chunks to download. Sit back and grab a coffee if you may like :)")
        for row in links:
            try:
                proc = subprocess.Popen("wget '" + row[:-1] + "' -O temp_chunks/'" + str(chunk_num) + ".mp4' ", stdout=subprocess.PIPE, shell=True)
                proc.wait()
                (stdout, stderr) = proc.communicate()
                if proc.returncode != 0:
                    print(str(stdout, 'utf-8'))
                    error_flag = 1
                    print("Couldn't Download----------->\n")
                    print("An error occurred while getting " + row[:-1])
                    break
                else:
                    print(str(stdout, 'utf-8'))
                chunk_num += 1
            except Exception as e:
                print("An error occurred while getting " + row[:-1])
                print(e)
                error_flag = 1
                subprocess.call("rm -rf temp_chunks", shell=True)
                break
        if error_flag == 0:
            if output_dir is "":
                if filename == "":
                    save_file = open('file.mp4', 'ab')
                else:
                    save_file = open(filename, 'ab')
            else:
                if filename == "":
                    if str(output_dir).endswith("/"):
                        save_file = open(output_dir + "file.mp4", 'ab')
                    else:
                        save_file = open(output_dir + "/file.mp4", 'ab')

                else:
                    if str(output_dir).endswith("/"):
                        save_file = open(output_dir + filename, 'ab')
                    else:
                        save_file = open(output_dir + "/" + filename, 'ab')

            for i in range(0, len(links)):
                f = open('temp_chunks/' + str(i) + ".mp4", 'rb')
                save_file.write(f.read())
                f.close()
            save_file.close()
            print("Done Mixin!")
            subprocess.call("rm -rf temp_chunks", shell=True)
            print("Success!")


def main():
    argv = sys.argv[1:]
    opts = []
    try:
        opts, args = getopt.getopt(argv, "p:b:O:n:", ["path=", "base-link=", "output=", "filename="])
    except Exception as e:
        print(e)
        opts = []
    path = ""
    base_link = ""
    output_dir = ""
    filename = ""
    for opt, arg in opts:
        if opt == "-p" or opt == "--path":
            path = arg
        if opt == "-b" or opt == "--base-link":
            base_link = arg
        if opt == "-O" or opt == "--output":
            output_dir = arg
        if opt == "-n" or opt == "--filename":
            filename = arg

    fetch_m3u8(path, base_link, output_dir, filename)


if __name__ == "__main__":
    main()
