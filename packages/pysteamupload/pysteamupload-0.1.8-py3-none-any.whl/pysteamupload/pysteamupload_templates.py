APP_BUILD = """
"appbuild"
{
    "appid"	"" // steam application id
    "desc" "" // description for this build
    "buildoutput" "" // build output folder for .log, .csm & .csd files, relative to location of this file
    "contentroot" "" // root content folder, relative to location of this file
    "setlive"	"" // branch to set live after successful build, non if empty
    "preview" "0" // to enable preview builds
    "local"	""	// set to file path of local content server

    "depots"
    {
    }
}
"""

DEPOT = """
"DepotBuildConfig"
{
    "DepotID" ""

    // Set a root for all content.
    // All relative paths specified below (LocalPath in FileMapping entries, and FileExclusion paths)
    // will be resolved relative to this root.
    // If you don't define ContentRoot, then it will be assumed to be
    // the location of this script file, which probably isn't what you want

    // include all files recursively
    "FileMapping"
    {
        // This can be a full path, or a path relative to ContentRoot
        "LocalPath" "*"

        // This is a path relative to the install folder of your game
        "DepotPath" "."

        // If LocalPath contains wildcards, setting this means that all
        // matching files within subdirectories of LocalPath will also
        // be included.
        "recursive" "1"
    }
}
"""
