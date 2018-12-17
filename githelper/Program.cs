using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using CommandLine;

namespace GitHelper
{
    public class Options
    {
        [Option('v', "verbose", Required = false, HelpText = "Set output to verbose mode")]
        public bool Verbose { get; set; }

        [Option('g', "git-directory", Required =true, HelpText = "The location of the git directory to compare to")]
        public string GitDirectory { get; set; }

        [Option('u', "untracked-directory", Required =true, HelpText = "The location of the untracked directory to compare against git")]
        public string UntrackedDirectory { get; set; }
    }

    public class DirectoryListing
    {
        public bool Include { get; set; }
        public string DirectoryPath { get; set; }
    }
    class Program
    {
        static void Main(string[] args)
        {
            CommandLine.Parser.Default.ParseArguments<Options>(args)
                .WithParsed<Options>(opts =>
                    {
                        var untrackedDirectories = Directory.GetDirectories(opts.UntrackedDirectory, "*", SearchOption.AllDirectories);
                        var trackedDirectories =
                            Directory.GetDirectories(opts.GitDirectory, "*", SearchOption.AllDirectories);

                        if (opts.Verbose)
                        {
                            Console.WriteLine(FormatMessage("VERBOSE", $"Found {untrackedDirectories.Length} Untracked Directories"));
                            Console.WriteLine(FormatMessage("VERBOSE", $"Found {trackedDirectories.Length} Git Tracked Directories"));
                        }

                        var normalizedUntrackedDirectories =
                            NormalizePaths(opts.UntrackedDirectory, untrackedDirectories);

                        var normalizedTrackedDirectories = NormalizePaths(opts.GitDirectory, trackedDirectories);

                        var directoryList = normalizedUntrackedDirectories.Except(normalizedTrackedDirectories).ToList();
                        var finalList = new List<DirectoryListing>();


                        directoryList.ForEach(d =>
                        {
                            var parent = Path.GetDirectoryName(d);

                            var listing = new DirectoryListing
                            {
                                Include = true,
                                DirectoryPath = d
                            };

                            if (directoryList.Any(pd => pd == parent))
                                listing.Include = false;

                            finalList.Add(listing);
                        });


                        foreach (var dl in finalList.Where(l => l.Include == true))
                        {
                            Console.WriteLine(Path.Join("/src/Files", dl.DirectoryPath.Replace("\\", "/")));
                        }
                    });

            Console.ReadLine();
        }

        private static List<string> NormalizePaths(string parentPath, string[] directories)
        {
            var dirList = directories.ToList();
            var normalized = new List<string>();

            dirList.ForEach(d => normalized.Add(d.Replace(parentPath, "")));

            return normalized;
        }

        static string FormatMessage(string type, string message)
        {
            return $"{DateTime.Now.ToString("s")} ${type} ${message}";
        }
    }
}
